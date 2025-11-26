import { clsx } from 'clsx';
import type { CEFRLevel } from '@/types';

interface SkillCardProps {
  skill: string;
  level: CEFRLevel;
  icon: React.ReactNode;
}

const levelColors: Record<CEFRLevel, string> = {
  A1: 'bg-red-100 text-red-700',
  A2: 'bg-orange-100 text-orange-700',
  B1: 'bg-yellow-100 text-yellow-700',
  B2: 'bg-green-100 text-green-700',
  C1: 'bg-blue-100 text-blue-700',
  C2: 'bg-purple-100 text-purple-700',
};

const levelProgress: Record<CEFRLevel, number> = {
  A1: 16.67,
  A2: 33.33,
  B1: 50,
  B2: 66.67,
  C1: 83.33,
  C2: 100,
};

export function SkillCard({ skill, level, icon }: SkillCardProps) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-gray-500">{icon}</span>
          <span className="font-medium text-gray-700">{skill}</span>
        </div>
        <span className={clsx('px-2 py-0.5 rounded-full text-sm font-bold', levelColors[level])}>
          {level}
        </span>
      </div>
      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-primary-500 rounded-full transition-all duration-500"
          style={{ width: `${levelProgress[level]}%` }}
        />
      </div>
    </div>
  );
}

export default SkillCard;
