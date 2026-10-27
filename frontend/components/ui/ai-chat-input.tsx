import { useEffect, useRef, useState, useMemo } from "react";
import { ArrowUp, CheckCircle2, Sparkles } from "lucide-react";
import rawCatalog from "@/lib/civicCatalog.json";
import { cn } from "@/lib/utils";

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmitSuggestion?: (suggestion: string) => void;
  disabled?: boolean;
  placeholder?: string;
  className?: string;
}

export function PromptInput({
  value,
  onChange,
  onSubmitSuggestion,
  disabled = false,
  placeholder = "Describe what you need to do (e.g. birth certificate, trade license, water connection)...",
  className,
}: PromptInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "0px";
    const height = Math.min(textarea.scrollHeight, 160);
    textarea.style.height = `${Math.max(height, 24)}px`;
    textarea.style.overflowY = textarea.scrollHeight > 160 ? "auto" : "hidden";
  }, [value]);

  // Check matching civic services in real time as the user types
  const matchedServices = useMemo(() => {
    const query = value.toLowerCase().trim();
    if (!query || query.length < 2) return [];

    return rawCatalog.filter((item) => {
      const q = query;
      return (
        item.name.toLowerCase().includes(q) ||
        item.id.toLowerCase().includes(q) ||
        item.summary.toLowerCase().includes(q)
      );
    }).slice(0, 3);
  }, [value]);

  return (
    <div className="relative w-full">
      {/* Real-time verified procedure suggestions dropdown */}
      {showSuggestions && matchedServices.length > 0 && (
        <div className="absolute bottom-full left-0 right-0 mb-2 overflow-hidden rounded-xl border border-brand-200/80 bg-white/95 p-1.5 shadow-xl backdrop-blur-md animate-enter z-20">
          <div className="flex items-center gap-1.5 px-2 py-1 text-[11px] font-semibold text-brand-700">
            <Sparkles className="h-3 w-3" />
            <span>Verified Civic Procedures matched:</span>
          </div>
          <div className="flex flex-col gap-1">
            {matchedServices.map((service) => (
              <button
                key={service.id}
                type="button"
                onMouseDown={(e) => {
                  e.preventDefault();
                  const prompt = `How do I apply for ${service.name}? What are the required documents and steps?`;
                  onChange(prompt);
                  if (onSubmitSuggestion) {
                    onSubmitSuggestion(prompt);
                  }
                  setShowSuggestions(false);
                }}
                className="group flex items-center justify-between rounded-lg px-2.5 py-1.5 text-left text-xs transition hover:bg-brand-50"
              >
                <div className="flex items-center gap-1.5 min-w-0">
                  <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-emerald-600" />
                  <span className="truncate font-medium text-slate-800 group-hover:text-brand-800">
                    {service.name}
                  </span>
                </div>
                <span className="shrink-0 rounded-full bg-slate-100 px-2 py-0.5 text-[10px] text-slate-500 group-hover:bg-brand-100 group-hover:text-brand-700">
                  {service.category}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      <div
        className={cn(
          "w-full rounded-2xl border border-slate-200 bg-white shadow-sm transition-colors focus-within:border-brand-700/40 focus-within:ring-2 focus-within:ring-brand-700/10",
          disabled && "opacity-70",
          className
        )}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onChange={(event) => {
            onChange(event.target.value);
            setShowSuggestions(true);
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              setShowSuggestions(false);
              event.currentTarget.form?.requestSubmit();
            }
          }}
          placeholder={placeholder}
          aria-label="Describe what you need to do"
          disabled={disabled}
          rows={1}
          className="block max-h-40 min-h-12 w-full resize-none bg-transparent px-4 pb-2 pt-3 text-sm leading-6 text-slate-900 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed"
        />
        <div className="flex items-center justify-between gap-3 px-3 pb-2">
          <div className="flex items-center gap-1.5 text-[11px] text-slate-500">
            {matchedServices.length > 0 ? (
              <span className="inline-flex items-center gap-1 font-medium text-emerald-700">
                <CheckCircle2 className="h-3 w-3 text-emerald-600" />
                Verified procedure matched ({matchedServices.length})
              </span>
            ) : (
              <span>NagarSetu · 101 Verified Civic Services</span>
            )}
          </div>
          <button
            type="submit"
            disabled={disabled || !value.trim()}
            aria-label="Send chat message"
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-700 text-white transition-colors hover:bg-brand-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ArrowUp aria-hidden="true" className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
