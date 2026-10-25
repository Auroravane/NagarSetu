"use client";

import Image from "next/image";
import { motion, useScroll, useTransform, useReducedMotion } from "framer-motion";

export function CivicMapBackground() {
  const prefersReducedMotion = useReducedMotion();
  const { scrollYProgress } = useScroll();

  // Subtle scroll-linked pan & gentle scale across the page scroll
  const translateY = useTransform(scrollYProgress, [0, 1], ["0%", "-6%"]);
  const scale = useTransform(scrollYProgress, [0, 1], [1, 1.05]);

  return (
    <div
      aria-label="Map of India highlighting Punjab and Chandigarh"
      role="img"
      className="pointer-events-none fixed inset-0 z-0 overflow-hidden bg-[#e9f9fc]"
    >
      <motion.div
        className="civic-map-zoom absolute inset-0"
        style={
          prefersReducedMotion
            ? { scale: 1, translateY: "0%" }
            : { scale, translateY }
        }
      >
        <Image
          src="/nagarsetu-civic-map.png"
          alt="Civic Map Background"
          fill
          priority
          sizes="100vw"
          className="object-cover object-center opacity-70 mix-blend-multiply"
        />
      </motion.div>
      <div className="absolute inset-0 bg-gradient-to-br from-white/50 via-white/60 to-sky-50/45" />
      {[
        { name: "Punjab", className: "civic-map-punjab" },
        { name: "Haryana", className: "civic-map-haryana" },
      ].map((region) => (
        <motion.div
          key={region.name}
          aria-hidden="true"
          className={`${region.className} absolute h-8 w-8 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-brand-700/70`}
          initial={{ opacity: 0.5, scale: 0.9 }}
          animate={
            prefersReducedMotion
              ? { opacity: 0.7, scale: 1 }
              : { opacity: [0.4, 0.85, 0.4], scale: [0.9, 1.15, 0.9] }
          }
          transition={
            prefersReducedMotion
              ? { duration: 0 }
              : { duration: 3.5, repeat: Infinity, ease: "easeInOut" }
          }
        >
          <span className="absolute inset-1 rounded-full bg-brand-700/20" />
        </motion.div>
      ))}
    </div>
  );
}
