import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';
import { Label } from '../ui/label';
import { User, Mail, Calendar, Trophy, Star, Flame } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="container py-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Profile</h1>
        <p className="text-muted-foreground mt-2">
          Your account information and statistics
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Account Info */}
        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
            <CardDescription>Your basic account details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Display Name
              </Label>
              <p className="text-sm">{user.display_name || 'Not set'}</p>
            </div>

            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </Label>
              <p className="text-sm">{user.email}</p>
            </div>

            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                Member Since
              </Label>
              <p className="text-sm">
                {new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Stats</CardTitle>
            <CardDescription>Your learning progress at a glance</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Star className="h-4 w-4 text-yellow-500" />
                <span className="text-sm">Points</span>
              </div>
              <span className="text-xl font-bold">{user.points}</span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Trophy className="h-4 w-4 text-blue-500" />
                <span className="text-sm">Level</span>
              </div>
              <Badge variant="secondary">Level {user.level}</Badge>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Flame className="h-4 w-4 text-orange-500" />
                <span className="text-sm">Streak</span>
              </div>
              <span className="text-xl font-bold">{user.streak_days} days</span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Trophy className="h-4 w-4 text-purple-500" />
                <span className="text-sm">Badges</span>
              </div>
              <span className="text-xl font-bold">{user.badges?.length || 0}</span>
            </div>
          </CardContent>
        </Card>

        {/* Activity Summary */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Activity Summary</CardTitle>
            <CardDescription>Total activities completed</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{user.qa_count || 0}</div>
                <div className="text-sm text-muted-foreground mt-1">Questions</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{user.summarize_count || 0}</div>
                <div className="text-sm text-muted-foreground mt-1">Summaries</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{user.mcq_count || 0}</div>
                <div className="text-sm text-muted-foreground mt-1">MCQs</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{user.code_explain_count || 0}</div>
                <div className="text-sm text-muted-foreground mt-1">Code Explains</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{user.code_fix_count || 0}</div>
                <div className="text-sm text-muted-foreground mt-1">Code Fixes</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
