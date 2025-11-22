import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';
import { MessageSquare, FileText, ListChecks, Code2, Wrench } from 'lucide-react';

export default function UserStats({ stats }) {
  const activities = [
    { 
      label: 'Questions Asked', 
      count: stats.activities_breakdown.qa, 
      icon: MessageSquare,
      color: 'text-blue-500'
    },
    { 
      label: 'Documents Summarized', 
      count: stats.activities_breakdown.summarize, 
      icon: FileText,
      color: 'text-green-500'
    },
    { 
      label: 'MCQs Generated', 
      count: stats.activities_breakdown.mcq, 
      icon: ListChecks,
      color: 'text-purple-500'
    },
    { 
      label: 'Code Analyzed', 
      count: stats.activities_breakdown.code_explain, 
      icon: Code2,
      color: 'text-orange-500'
    },
    { 
      label: 'Code Fixes', 
      count: stats.activities_breakdown.code_fix, 
      icon: Wrench,
      color: 'text-red-500'
    }
  ];

  const featureUnlocks = [
    { name: 'Max File Size', value: `${stats.feature_unlocks.max_file_size / 1000}K chars` },
    { name: 'Max MCQ Questions', value: stats.feature_unlocks.max_mcq_questions },
    { name: 'Max Summary Points', value: stats.feature_unlocks.max_summary_points }
  ];

  return (
    <div className="space-y-6">
      {/* Activity Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Activity Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {activities.map((activity, idx) => {
              const Icon = activity.icon;
              const percentage = (activity.count / stats.total_activities) * 100 || 0;
              
              return (
                <div key={idx} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Icon className={`h-4 w-4 ${activity.color}`} />
                      <span className="text-sm font-medium">{activity.label}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      {activity.count}
                    </span>
                  </div>
                  <Progress value={percentage} className="h-2" />
                </div>
              );
            })}
          </div>

          <div className="mt-6 pt-6 border-t">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium">Total Activities</span>
              <span className="text-2xl font-bold">{stats.total_activities}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Feature Unlocks */}
      <Card>
        <CardHeader>
          <CardTitle>Feature Unlocks</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {featureUnlocks.map((feature, idx) => (
              <div key={idx} className="p-4 bg-muted rounded-lg text-center">
                <div className="text-2xl font-bold">{feature.value}</div>
                <div className="text-sm text-muted-foreground mt-1">{feature.name}</div>
              </div>
            ))}
          </div>

          <div className="mt-4 text-sm text-muted-foreground">
            💡 Earn more points to unlock bigger limits!
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
