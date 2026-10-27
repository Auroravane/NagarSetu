"use client";

import React, { useState, useTransition, useMemo, useRef, useEffect } from "react";
import { Search, Tag, X, Clock, IndianRupee, ArrowRight, Sparkles } from "lucide-react";
import rawCatalog from "@/lib/civicCatalog.json";
import { cn } from "@/lib/utils";

export interface CivicProcedureItem {
  id: string;
  name: string;
  summary: string;
  category: string;
  time: string;
  cost: string;
}

const CATEGORIES = [
  "All",
  "Business & Licenses",
  "Utilities & Water",
  "Property & Revenue",
  "Certificates & Identity",
  "Transport & Vehicles",
  "Welfare & Schemes",
] as const;

type CategoryType = (typeof CATEGORIES)[number];

interface CivicSearchHeaderProps {
  onSelectProcedure: (procedure: CivicProcedureItem, queryPrompt?: string) => void;
  className?: string;
}

export function CivicSearchHeader({ onSelectProcedure, className }: CivicSearchHeaderProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<CategoryType>("All");
  const [isOpen, setIsOpen] = useState(false);
  const [, startTransition] = useTransition();
  const dropdownRef = useRef<HTMLDivElement>(null);

  const catalog: CivicProcedureItem[] = rawCatalog as CivicProcedureItem[];

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredProcedures = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return catalog.filter((item) => {
      const matchesCategory =
        selectedCategory === "All" || item.category === selectedCategory;
      const matchesQuery =
        !q ||
        item.name.toLowerCase().includes(q) ||
        item.summary.toLowerCase().includes(q) ||
        item.id.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q);
      return matchesCategory && matchesQuery;
    });
  }, [catalog, searchQuery, selectedCategory]);

  const handleSelect = (item: CivicProcedureItem) => {
    setIsOpen(false);
    setSearchQuery("");
    const prompt = `How do I apply for ${item.name}? What are the required documents and steps?`;
    onSelectProcedure(item, prompt);
  };

  return (
    <div ref={dropdownRef} className={cn("relative w-full max-w-2xl", className)}>
      {/* Search Input Bar */}
      <div className="relative flex items-center">
        <div className="pointer-events-none absolute left-3 flex items-center text-slate-400">
          <Search className="h-4 w-4 text-brand-600" />
        </div>
        <input
          type="text"
          value={searchQuery}
          onFocus={() => setIsOpen(true)}
          onChange={(e) => {
            const val = e.target.value;
            startTransition(() => {
              setSearchQuery(val);
            });
            setIsOpen(true);
          }}
          placeholder="Search 100+ civic services (e.g. FSSAI food, trade license, water, birth certificate, driving license)..."
          className="h-9 w-full rounded-full border border-slate-200 bg-slate-50/90 pl-9 pr-8 text-xs text-slate-800 placeholder-slate-400 shadow-inner transition-all duration-200 hover:border-slate-300 hover:bg-white focus:border-brand-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-500/20 sm:text-xs"
        />
        {searchQuery ? (
          <button
            type="button"
            onClick={() => {
              setSearchQuery("");
            }}
            className="absolute right-2.5 flex h-5 w-5 items-center justify-center rounded-full text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            title="Clear search"
          >
            <X className="h-3 w-3" />
          </button>
        ) : (
          <div className="pointer-events-none absolute right-2.5 hidden items-center gap-1 rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-semibold text-slate-500 sm:flex">
            <span>101 Services</span>
          </div>
        )}
      </div>

      {/* Dropdown Menu with Category Filter Pills & Results */}
      {isOpen && (
        <div className="absolute left-0 right-0 top-11 z-50 max-h-[460px] overflow-hidden rounded-2xl border border-slate-200/90 bg-white/95 shadow-2xl backdrop-blur-md animate-enter">
          {/* Category Filter Pills Bar - horizontal scroll without bulky OS scrollbar */}
          <div className="flex items-center gap-1.5 overflow-x-auto border-b border-slate-100 p-2.5 no-scrollbar">
            {CATEGORIES.map((cat) => {
              const active = selectedCategory === cat;
              return (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  className={cn(
                    "shrink-0 whitespace-nowrap rounded-full px-2.5 py-1 text-[11px] font-medium transition-colors",
                    active
                      ? "bg-brand-700 text-white shadow-xs"
                      : "bg-slate-100/80 text-slate-600 hover:bg-slate-200/70 hover:text-slate-900"
                  )}
                >
                  {cat}
                </button>
              );
            })}
          </div>

          {/* Results List - sleek custom vertical scrollbar */}
          <div className="max-h-[360px] overflow-y-auto divide-y divide-slate-100 p-1.5 custom-scrollbar">
            {filteredProcedures.length === 0 ? (
              <div className="px-4 py-8 text-center text-xs text-slate-500">
                <p>No civic procedure found matching &ldquo;{searchQuery}&rdquo;.</p>
                <p className="mt-1 text-[11px] text-slate-400">
                  Try terms like &ldquo;trade&rdquo;, &ldquo;food&rdquo;, &ldquo;water&rdquo;, &ldquo;pension&rdquo;, or &ldquo;vehicle&rdquo;.
                </p>
              </div>
            ) : (
              filteredProcedures.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => handleSelect(item)}
                  className="group flex w-full flex-col items-start gap-1 rounded-xl p-2.5 text-left transition hover:bg-brand-50/70"
                >
                  <div className="flex w-full items-center justify-between gap-2">
                    <span className="font-semibold text-xs text-slate-900 group-hover:text-brand-800">
                      {item.name}
                    </span>
                    <span className="shrink-0 rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600 group-hover:bg-brand-100 group-hover:text-brand-700">
                      {item.category}
                    </span>
                  </div>
                  <p className="line-clamp-2 text-[11px] text-slate-500 leading-snug">
                    {item.summary}
                  </p>
                  <div className="mt-1 flex items-center gap-3 text-[10px] text-slate-400">
                    {item.time && (
                      <span className="inline-flex items-center gap-1">
                        <Clock className="h-3 w-3 text-slate-400" />
                        {item.time}
                      </span>
                    )}
                    {item.cost && (
                      <span className="inline-flex items-center gap-1">
                        <IndianRupee className="h-3 w-3 text-slate-400" />
                        {item.cost}
                      </span>
                    )}
                    <span className="ml-auto inline-flex items-center gap-0.5 text-[10px] font-medium text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity">
                      Ask AI <ArrowRight className="h-2.5 w-2.5" />
                    </span>
                  </div>
                </button>
              ))
            )}
          </div>

          {/* Footer note */}
          <div className="flex items-center justify-between border-t border-slate-100 bg-slate-50/80 px-3 py-1.5 text-[11px] text-slate-500">
            <span className="inline-flex items-center gap-1">
              <Sparkles className="h-3 w-3 text-brand-600" />
              Showing {filteredProcedures.length} of {catalog.length} verified procedures
            </span>
            <span className="text-[10px] text-slate-400">Click to run AI query</span>
          </div>
        </div>
      )}
    </div>
  );
}
