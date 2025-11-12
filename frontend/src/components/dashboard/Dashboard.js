import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Trophy, Star, Flame, TrendingUp, Award, Zap } from 'lucide-react';
import axios from 'axios';
import UserStats from '../gamification/UserStats';
import Leaderboard from '../gamification/Leaderboard';
import BadgeDisplay from '../gamification/BadgeDisplay';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export default function Dashboard() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchStats();
    }
  }, [token]);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v3/gamification/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container py-8">
        <div className="animate-pulse space-y-4">
          <div className="h-32 bg-muted rounded-lg"></div>
          <div className="h-64 bg-muted rounded-lg"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8 space-y-8">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Welcome back, {user?.display_name || 'Learner'}!
          </h1>
          <p className="text-muted-foreground mt-1">
            Keep up the great work! 🎓
          </p>
        </div>
      </div>

      {/* Quick Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total Points</CardTitle>
              <Star className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.points}</div>
              <p className="text-xs text-muted-foreground mt-1">
                Rank #{stats.rank || 'N/A'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Level</CardTitle>
              <TrendingUp className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats.level} - {stats.level_name}
              </div>
              <Progress 
                value={(stats.points / (stats.points + stats.points_to_next_level)) * 100} 
                className="mt-2"
              />
              <p className="text-xs text-muted-foreground mt-1">
                {stats.points_to_next_level} pts to next level
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Badges</CardTitle>
              <Award className="h-4 w-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.badges.length}</div>
              <p className="text-xs text-muted-foreground mt-1">
                {9 - stats.badges.length} more to collect
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Streak</CardTitle>
              <Flame className="h-4 w-4 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.streak_days} days</div>
              <p className="text-xs text-muted-foreground mt-1">
                Keep it going! 🔥
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="badges">Badges</TabsTrigger>
          <TabsTrigger value="leaderboard">Leaderboard</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          {stats && <UserStats stats={stats} />}
        </TabsContent>

        <TabsContent value="badges" className="space-y-4">
          {stats && <BadgeDisplay badges={stats.badges} allBadges={getAllBadges()} />}
        </TabsContent>

        <TabsContent value="leaderboard" className="space-y-4">
          <Leaderboard token={token} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

// Badge definitions
function getAllBadges() {
  return [
    { id: 'beginner', name: '🏆 Beginner', description: 'Complete your first activity' },
    { id: 'reader', name: '📚 Reader', description: 'Summarize 10 documents' },
    { id: 'scholar', name: '🎓 Scholar', description: 'Summarize 50 documents' },
    { id: 'coder', name: '💻 Coder', description: 'Analyze 20 code files' },
    { id: 'debugger', name: '🐛 Debugger', description: 'Fix 10 code errors' },
    { id: 'streak_master', name: '🔥 Streak Master', description: '30-day activity streak' },
    { id: 'quiz_master', name: '🎯 Quiz Master', description: 'Generate 50 quizzes' },
    { id: 'speed_learner', name: '⚡ Speed Learner', description: 'Ask 100 questions' },
    { id: 'legend', name: '👑 Legend', description: 'Reach 10,000 points' }
  ];
}
