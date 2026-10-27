"use client";

import { ExternalLink, FileText } from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import type { SourceRef } from "@/lib/types";

interface SourcePopoverProps {
  chunkId: string;
  sources: SourceRef[];
}

export function SourcePopover({ chunkId, sources }: SourcePopoverProps) {
  const source = sources.find((s) => s.chunk_id === chunkId);
  if (!source) {
    return <span className="text-[11px] text-slate-500">[{chunkId}]</span>;
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button
          type="button"
          className="inline-flex items-center gap-1 rounded-md bg-brand-50 px-2.5 py-1 text-xs font-medium text-brand-700 transition-colors duration-150 ease-out hover:bg-brand-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
        >
          <FileText aria-hidden="true" className="h-3 w-3" />
          Source
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-80 text-left">
        {source.title && (
          <h4 className="text-xs font-semibold text-slate-900">{source.title}</h4>
        )}
        {(source.department || source.jurisdiction) && (
          <div className="mt-1 flex flex-wrap gap-1 text-[10px] text-slate-500">
            {source.department && <span className="rounded bg-slate-100 px-1.5 py-0.5">{source.department}</span>}
            {source.jurisdiction && <span className="rounded bg-slate-100 px-1.5 py-0.5">{source.jurisdiction}</span>}
          </div>
        )}
        <p className="mt-2 text-xs leading-relaxed text-slate-700">{source.snippet}</p>
        <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500">
          <span className="font-mono text-[10px] text-slate-400">{source.chunk_id}</span>
          {source.last_verified && <span>Verified: {source.last_verified}</span>}
        </div>
        {source.source_url && source.source_url !== "MOCK" ? (
          <a
            href={source.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-brand-700 hover:underline"
          >
            Open official document
            <ExternalLink aria-hidden="true" className="h-3 w-3" />
          </a>
        ) : (
          <p className="mt-2 text-[11px] italic text-slate-500">
            Official doc verification pending / Demo fixture
          </p>
        )}
      </PopoverContent>
    </Popover>
  );
}
