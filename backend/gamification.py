"""
Gamification Service
Handles points, badges, levels, leaderboards, feature unlocks
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bson import ObjectId

from models.user import UserInDB, UserStats
from models.activity import (
    Activity, ACTIVITY_POINTS, BADGES, LEVELS, FEATURE_UNLOCKS
)

logger = logging.getLogger(__name__)


class GamificationService:
    """Gamification service for points, badges, levels"""
    
    def __init__(self, db=None):
        self.db = db
        self.mongodb_available = db is not None
    
    async def log_activity(
        self,
        user_id: str,
        activity_type: str,
        metadata: dict = None
    ) -> Dict:
        """
        Log user activity and award points
        Returns: {points_earned, new_badges, level_up, feature_unlocks}
        """
        if not self.mongodb_available:
            logger.warning("Activity logging skipped - MongoDB not available")
            return {"points_earned": 0, "new_badges": [], "level_up": False}
        
        # Get points for activity
        points = ACTIVITY_POINTS.get(activity_type, 0)
        
        # Get user
        user_data = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            logger.error(f"User not found: {user_id}")
            return {"points_earned": 0, "new_badges": [], "level_up": False}
        
        user = UserInDB(**user_data)
        old_points = user.points
        old_level = user.level
        
        # Update streak
        streak_bonus = await self._update_streak(user)
        points += streak_bonus
        
        # Update user stats
        new_points = user.points + points
        activity_count_field = f"{activity_type}_count"
        
        update_data = {
            "$set": {
                "points": new_points,
                "last_activity_date": datetime.utcnow()
            },
            "$inc": {
                "total_activities": 1,
                activity_count_field: 1
            }
        }
        
        await self.db.users.update_one({"_id": ObjectId(user_id)}, update_data)
        
        # Log activity
        activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            points_earned=points,
            metadata=metadata or {}
        )
        await self.db.activities.insert_one(activity.dict(by_alias=True, exclude={"id"}))
        
        # Check for new level
        new_level = self._calculate_level(new_points)
        level_up = new_level > old_level
        if level_up:
            await self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"level": new_level}}
            )
            logger.info(f"User {user_id} leveled up to {new_level}")
        
        # Check for new badges
        user_data = await self.db.users.find_one({"_id": ObjectId(user_id)})
        user = UserInDB(**user_data)
        new_badges = await self._check_badges(user)
        
        # Check for feature unlocks
        new_unlocks = await self._check_feature_unlocks(user)
        
        return {
            "points_earned": points,
            "new_badges": new_badges,
            "level_up": level_up,
            "new_level": new_level if level_up else old_level,
            "feature_unlocks": new_unlocks
        }
    
    async def _update_streak(self, user: UserInDB) -> int:
        """Update user's activity streak and return bonus points"""
        today = datetime.utcnow().date()
        bonus = 0
        
        if user.last_activity_date:
            last_activity = user.last_activity_date.date()
            days_diff = (today - last_activity).days
            
            if days_diff == 0:
                # Same day, no streak update
                return 0
            elif days_diff == 1:
                # Consecutive day, increment streak
                new_streak = user.streak_days + 1
                await self.db.users.update_one(
                    {"_id": user.id},
                    {"$set": {"streak_days": new_streak}}
                )
                
                # Award bonus for milestones
                if new_streak == 7:
                    bonus = ACTIVITY_POINTS["streak_7"]
                    logger.info(f"User {user.id} reached 7-day streak")
                elif new_streak == 30:
                    bonus = ACTIVITY_POINTS["streak_30"]
                    logger.info(f"User {user.id} reached 30-day streak")
            else:
                # Streak broken, reset
                await self.db.users.update_one(
                    {"_id": user.id},
                    {"$set": {"streak_days": 1}}
                )
                logger.info(f"User {user.id} streak reset")
        else:
            # First activity
            await self.db.users.update_one(
                {"_id": user.id},
                {"$set": {"streak_days": 1}}
            )
        
        return bonus
    
    def _calculate_level(self, points: int) -> int:
        """Calculate user level based on points"""
        for level_data in LEVELS:
            if level_data["min_points"] <= points <= level_data["max_points"]:
                return level_data["level"]
        return LEVELS[-1]["level"]  # Max level
    
    def _get_level_name(self, level: int) -> str:
        """Get level name"""
        for level_data in LEVELS:
            if level_data["level"] == level:
                return level_data["name"]
        return "Master"
    
    def _points_to_next_level(self, points: int, level: int) -> int:
        """Calculate points needed for next level"""
        if level >= len(LEVELS):
            return 0  # Max level
        
        next_level = level + 1
        for level_data in LEVELS:
            if level_data["level"] == next_level:
                return max(0, level_data["min_points"] - points)
        return 0
    
    async def _check_badges(self, user: UserInDB) -> List[str]:
        """Check and award new badges"""
        new_badges = []
        
        for badge_id, badge_data in BADGES.items():
            if badge_id in user.badges:
                continue  # Already has badge
            
            req = badge_data["requirement"]
            req_type = req["type"]
            req_count = req["count"]
            
            # Check requirement
            earned = False
            if req_type == "total_activities":
                earned = user.total_activities >= req_count
            elif req_type == "summarize_count":
                earned = user.summarize_count >= req_count
            elif req_type == "code_explain_count":
                earned = user.code_explain_count >= req_count
            elif req_type == "code_fix_count":
                earned = user.code_fix_count >= req_count
            elif req_type == "mcq_count":
                earned = user.mcq_count >= req_count
            elif req_type == "qa_count":
                earned = user.qa_count >= req_count
            elif req_type == "streak_days":
                earned = user.streak_days >= req_count
            elif req_type == "points":
                earned = user.points >= req_count
            
            if earned:
                new_badges.append(badge_id)
                await self.db.users.update_one(
                    {"_id": user.id},
                    {"$push": {"badges": badge_id}}
                )
                logger.info(f"User {user.id} earned badge: {badge_id}")
        
        return new_badges
    
    async def _check_feature_unlocks(self, user: UserInDB) -> List[dict]:
        """Check and apply feature unlocks based on points"""
        new_unlocks = []
        
        for unlock_id, unlock_data in FEATURE_UNLOCKS.items():
            if user.points >= unlock_data["points"]:
                benefits = unlock_data["benefit"]
                
                # Check if already unlocked
                already_unlocked = True
                for key, value in benefits.items():
                    current_value = getattr(user, key, 0)
                    if current_value < value:
                        already_unlocked = False
                        break
                
                if not already_unlocked:
                    # Apply unlock
                    await self.db.users.update_one(
                        {"_id": user.id},
                        {"$set": benefits}
                    )
                    new_unlocks.append({
                        "name": unlock_data["name"],
                        "benefits": benefits
                    })
                    logger.info(f"User {user.id} unlocked: {unlock_id}")
        
        return new_unlocks
    
    async def get_user_stats(self, user_id: str) -> UserStats:
        """Get detailed user statistics"""
        if not self.mongodb_available:
            return None
        
        user_data = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return None
        
        user = UserInDB(**user_data)
        
        # Get badges with details
        badges_detailed = []
        for badge_id in user.badges:
            if badge_id in BADGES:
                badge_info = BADGES[badge_id]
                badges_detailed.append({
                    "id": badge_id,
                    "name": badge_info["name"],
                    "description": badge_info["description"]
                })
        
        # Get rank
        rank = await self._get_user_rank(user_id)
        
        return UserStats(
            points=user.points,
            level=user.level,
            level_name=self._get_level_name(user.level),
            points_to_next_level=self._points_to_next_level(user.points, user.level),
            badges=badges_detailed,
            streak_days=user.streak_days,
            total_activities=user.total_activities,
            activities_breakdown={
                "qa": user.qa_count,
                "summarize": user.summarize_count,
                "mcq": user.mcq_count,
                "code_explain": user.code_explain_count,
                "code_fix": user.code_fix_count
            },
            feature_unlocks={
                "max_file_size": user.max_file_size,
                "max_mcq_questions": user.max_mcq_questions,
                "max_summary_points": user.max_summary_points
            },
            rank=rank
        )
    
    async def _get_user_rank(self, user_id: str) -> Optional[int]:
        """Get user's rank on leaderboard"""
        if not self.mongodb_available:
            return None
        
        user_data = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return None
        
        user_points = user_data.get("points", 0)
        
        # Count users with more points
        higher_count = await self.db.users.count_documents({
            "points": {"$gt": user_points}
        })
        
        return higher_count + 1
    
    async def get_leaderboard(
        self,
        period: str = "monthly",
        limit: int = 10
    ) -> List[dict]:
        """
        Get leaderboard
        period: monthly, all_time
        """
        if not self.mongodb_available:
            return []
        
        # For monthly, filter by activities in current month
        if period == "monthly":
            # Get top users by activity this month
            start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            
            pipeline = [
                {
                    "$match": {
                        "timestamp": {"$gte": start_of_month}
                    }
                },
                {
                    "$group": {
                        "_id": "$user_id",
                        "monthly_points": {"$sum": "$points_earned"}
                    }
                },
                {"$sort": {"monthly_points": -1}},
                {"$limit": limit}
            ]
            
            monthly_leaders = await self.db.activities.aggregate(pipeline).to_list(limit)
            
            # Get user details
            leaderboard = []
            for rank, leader in enumerate(monthly_leaders, 1):
                user_data = await self.db.users.find_one({"_id": ObjectId(leader["_id"])})
                if user_data:
                    leaderboard.append({
                        "rank": rank,
                        "user_id": str(user_data["_id"]),
                        "display_name": user_data.get("display_name", "Anonymous"),
                        "points": leader["monthly_points"],
                        "level": user_data.get("level", 1)
                    })
        
        else:  # all_time
            # Get top users by total points
            users = await self.db.users.find().sort("points", -1).limit(limit).to_list(limit)
            
            leaderboard = []
            for rank, user_data in enumerate(users, 1):
                leaderboard.append({
                    "rank": rank,
                    "user_id": str(user_data["_id"]),
                    "display_name": user_data.get("display_name", "Anonymous"),
                    "points": user_data.get("points", 0),
                    "level": user_data.get("level", 1)
                })
        
        return leaderboard
