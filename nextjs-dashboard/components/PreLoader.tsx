"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

export default function PreLoader() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Preloader duration: 2.5 seconds
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-navy-deep via-purple-900 to-navy-deep z-50 flex items-center justify-center">
      {/* Animated background circles */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-primary/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-orange-accent/20 rounded-full blur-3xl animate-pulse delay-700"></div>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center gap-8">
        {/* Logos container */}
        <div className="flex items-center gap-6 animate-fadeIn">
          {/* Mastercard Symbol */}
          <div className="relative w-16 h-16 animate-bounce-slow">
            <Image
              src="/ma_symbol.svg"
              alt="Mastercard"
              width={64}
              height={64}
              className="object-contain"
            />
          </div>

          {/* X symbol */}
          <div className="text-white text-4xl font-light animate-pulse">×</div>

          {/* App Logo */}
          <div className="relative w-16 h-16 animate-bounce-slow delay-300">
            <Image
              src="/app-logo.png"
              alt="Data Nova"
              width={64}
              height={64}
              className="object-contain"
            />
          </div>
        </div>

        {/* Loading text */}
        <div className="text-center animate-fadeIn delay-500">
          <h2 className="text-2xl font-poppins font-bold text-white mb-2">
            Data Nova
          </h2>
          <p className="text-purple-200 text-sm">
            Powered by Mastercard Center for Inclusive Growth
          </p>
        </div>

        {/* Loading spinner */}
        <div className="flex gap-2 animate-fadeIn delay-700">
          <div className="w-3 h-3 bg-purple-primary rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-orange-accent rounded-full animate-bounce delay-150"></div>
          <div className="w-3 h-3 bg-purple-primary rounded-full animate-bounce delay-300"></div>
        </div>

        {/* Progress bar */}
        <div className="w-64 h-1 bg-white/10 rounded-full overflow-hidden mt-4">
          <div className="h-full bg-gradient-to-r from-purple-primary to-orange-accent animate-progress"></div>
        </div>
      </div>

      <style jsx>{`
        @keyframes bounce-slow {
          0%,
          100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }

        @keyframes progress {
          0% {
            width: 0%;
          }
          100% {
            width: 100%;
          }
        }

        .animate-bounce-slow {
          animation: bounce-slow 2s ease-in-out infinite;
        }

        .animate-progress {
          animation: progress 2.5s ease-out forwards;
        }

        .delay-150 {
          animation-delay: 150ms;
        }

        .delay-300 {
          animation-delay: 300ms;
        }

        .delay-500 {
          animation-delay: 500ms;
        }

        .delay-700 {
          animation-delay: 700ms;
        }
      `}</style>
    </div>
  );
}
