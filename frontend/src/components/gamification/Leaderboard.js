import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../ui/tabs';
import { Trophy, Medal, Award } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export default function Leaderboard({ token }) {
  const [monthlyLeaders, setMonthlyLeaders] = useState([]);
  const [allTimeLeaders, setAllTimeLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboards();
  }, []);

  const fetchLeaderboards = async () => {
    try {
      const [monthly, allTime] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/v3/gamification/leaderboard?period=monthly&limit=10`),
        axios.get(`${API_BASE_URL}/api/v3/gamification/leaderboard?period=all_time&limit=10`)
      ]);

      setMonthlyLeaders(monthly.data.leaderboard);
      setAllTimeLeaders(allTime.data.leaderboard);
    } catch (error) {
      console.error('Failed to fetch leaderboards:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return <Trophy className="h-5 w-5 text-yellow-500" />;
    if (rank === 2) return <Medal className="h-5 w-5 text-gray-400" />;
    if (rank === 3) return <Award className="h-5 w-5 text-orange-600" />;
    return <span className="text-muted-foreground">#{rank}</span>;
  };

  const LeaderboardList = ({ leaders }) => (
    <div className="space-y-2">
      {leaders.map((leader) => (
        <div
          key={leader.user_id}
          className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="w-8 flex items-center justify-center">
              {getRankIcon(leader.rank)}
            </div>
            <div>
              <div className="font-medium">{leader.display_name}</div>
              <div className="text-xs text-muted-foreground">
                Level {leader.level}
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="font-bold">{leader.points.toLocaleString()}</div>
            <div className="text-xs text-muted-foreground">points</div>
          </div>
        </div>
      ))}
    </div>
  );

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Leaderboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-muted rounded-lg"></div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Leaderboard</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="monthly">
          <TabsList className="w-full">
            <TabsTrigger value="monthly" className="flex-1">
              Monthly
            </TabsTrigger>
            <TabsTrigger value="all_time" className="flex-1">
              All Time
            </TabsTrigger>
          </TabsList>

          <TabsContent value="monthly" className="mt-4">
            {monthlyLeaders.length > 0 ? (
              <LeaderboardList leaders={monthlyLeaders} />
            ) : (
              <div className="text-center text-muted-foreground py-8">
                No rankings yet this month
              </div>
            )}
          </TabsContent>

          <TabsContent value="all_time" className="mt-4">
            {allTimeLeaders.length > 0 ? (
              <LeaderboardList leaders={allTimeLeaders} />
            ) : (
              <div className="text-center text-muted-foreground py-8">
                No rankings yet
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
