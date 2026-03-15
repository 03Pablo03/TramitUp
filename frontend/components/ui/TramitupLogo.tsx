"use client";

interface TramitupLogoProps {
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function TramitupLogo({ className = "", size = "md" }: TramitupLogoProps) {
  const sizeClasses = {
    sm: "w-6 h-6",
    md: "w-8 h-8", 
    lg: "w-12 h-12"
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <svg 
        className={`${sizeClasses[size]} text-blue-600`}
        viewBox="0 0 32 32" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Documento base */}
        <rect 
          x="6" 
          y="4" 
          width="20" 
          height="24" 
          rx="2" 
          fill="currentColor" 
          fillOpacity="0.1"
          stroke="currentColor" 
          strokeWidth="2"
        />
        
        {/* Líneas de texto */}
        <line x1="10" y1="10" x2="22" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        <line x1="10" y1="14" x2="20" y2="14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        <line x1="10" y1="18" x2="18" y2="18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        
        {/* Check mark */}
        <circle cx="19" cy="22" r="4" fill="currentColor"/>
        <path d="M17 22l1.5 1.5L21 21" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
      
      <span className="font-fraunces font-semibold text-blue-600 text-lg">
        Tramitup
      </span>
    </div>
  );
}