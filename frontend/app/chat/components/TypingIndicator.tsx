"use client";

export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 max-w-4xl mx-auto px-4 py-2">
      {/* Avatar del asistente */}
      <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
        <span className="text-white text-sm font-medium">T</span>
      </div>

      {/* Burbuja con typing animation */}
      <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
        <div className="flex items-center gap-1">
          <div className="flex space-x-1">
            <div 
              className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"
              style={{
                animationDelay: '0ms',
                animationDuration: '1.4s'
              }}
            ></div>
            <div 
              className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"
              style={{
                animationDelay: '200ms',
                animationDuration: '1.4s'
              }}
            ></div>
            <div 
              className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"
              style={{
                animationDelay: '400ms',
                animationDuration: '1.4s'
              }}
            ></div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse {
          0%, 60%, 100% {
            opacity: 0.3;
            transform: scale(1);
          }
          30% {
            opacity: 1;
            transform: scale(1.1);
          }
        }
        
        .animate-pulse {
          animation: pulse 1.4s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}