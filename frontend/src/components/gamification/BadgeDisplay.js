import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Lock } from 'lucide-react';

export default function BadgeDisplay({ badges, allBadges }) {
  const earnedBadgeIds = badges.map(b => b.id);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Badges ({badges.length}/9)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {allBadges.map((badge) => {
            const isEarned = earnedBadgeIds.includes(badge.id);
            
            return (
              <div
                key={badge.id}
                className={`p-4 rounded-lg border-2 transition-all ${
                  isEarned
                    ? 'border-primary bg-primary/5'
                    : 'border-muted bg-muted/30 opacity-60'
                }`}
              >
                <div className="flex items-center justify-center mb-2">
                  {isEarned ? (
                    <div className="text-4xl">{badge.name.split(' ')[0]}</div>
                  ) : (
                    <div className="text-4xl opacity-30">
                      <Lock className="h-8 w-8" />
                    </div>
                  )}
                </div>
                <div className="text-center">
                  <div className="font-semibold text-sm">
                    {badge.name.split(' ').slice(1).join(' ')}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {badge.description}
                  </div>
                  {isEarned && (
                    <Badge variant="secondary" className="mt-2">
                      Unlocked
                    </Badge>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
