'use client';

interface ScoreGaugeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  confidence?: string;
}

export function ScoreGauge({ score, size = 'md', showLabel = true, confidence }: ScoreGaugeProps) {
  // Calculate color based on score
  const getColor = (score: number) => {
    if (score >= 80) return '#22c55e'; // green
    if (score >= 60) return '#eab308'; // yellow
    if (score >= 40) return '#f97316'; // orange
    return '#ef4444'; // red
  };

  const getLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Work';
    return 'Poor';
  };

  const color = getColor(score);
  const label = getLabel(score);

  const sizeConfig = {
    sm: { width: 80, strokeWidth: 6, fontSize: 'text-lg' },
    md: { width: 120, strokeWidth: 8, fontSize: 'text-2xl' },
    lg: { width: 160, strokeWidth: 10, fontSize: 'text-4xl' },
  };

  const config = sizeConfig[size];
  const radius = (config.width - config.strokeWidth) / 2;
  const circumference = radius * Math.PI; // Half circle
  const progress = (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <svg
        width={config.width}
        height={config.width / 2 + 10}
        className="transform -rotate-180"
      >
        {/* Background arc */}
        <circle
          cx={config.width / 2}
          cy={config.width / 2}
          r={radius}
          fill="none"
          stroke="#374151"
          strokeWidth={config.strokeWidth}
          strokeDasharray={`${circumference} ${circumference}`}
          strokeLinecap="round"
        />
        {/* Progress arc */}
        <circle
          cx={config.width / 2}
          cy={config.width / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={config.strokeWidth}
          strokeDasharray={`${progress} ${circumference}`}
          strokeLinecap="round"
          className="transition-all duration-500"
        />
      </svg>

      <div className="relative -mt-8 text-center">
        <span className={`font-bold ${config.fontSize}`} style={{ color }}>
          {score}
        </span>
        <span className="text-gray-500 text-sm">/100</span>
      </div>

      {showLabel && (
        <div className="mt-2 text-center">
          <span className="text-sm font-medium" style={{ color }}>
            {label}
          </span>
          {confidence && (
            <span className="text-xs text-gray-500 block">
              {confidence} confidence
            </span>
          )}
        </div>
      )}
    </div>
  );
}
