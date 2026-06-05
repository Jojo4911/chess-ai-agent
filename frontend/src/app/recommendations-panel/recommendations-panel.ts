import { Component, Input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AskResponse, ToolCall } from '../models/agent.models';

@Component({
  selector: 'app-recommendations-panel',
  standalone: false,
  templateUrl: './recommendations-panel.html',
  styleUrls: ['./recommendations-panel.css'],
})
export class RecommendationsPanel {
  @Input() response: AskResponse | null = null;
  @Input() loading = false;
  @Input() error: string | null = null;

  constructor(private sanitizer: DomSanitizer) {}

  get moves(): ToolCall | undefined {
    return this.response?.tool_calls?.find(
      t => t.tool === 'get_opening_moves' || t.tool.includes('move')
    );
  }

  get evaluation(): ToolCall | undefined {
    return this.response?.tool_calls?.find(
      t => t.tool === 'evaluate_position' || t.tool.includes('evaluat')
    );
  }

  get videos(): ToolCall | undefined {
    return this.response?.tool_calls?.find(
      t => t.tool === 'find_videos' || t.tool.includes('video')
    );
  }

  safeHtml(raw: any): SafeHtml {
    const str = (raw === null || raw === undefined)
        ? ''
        : (typeof raw === 'string' ? raw : JSON.stringify(raw, null, 2));
    const withLinks = str.replace(
      /(https?:\/\/[^\s<]+)/g,
      '<a href="$1" target="_blank" rel="noopener">$1</a>'
    );
    const withBold = withLinks.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    const withBreaks = withBold.replace(/\n/g, '<br>');
    return this.sanitizer.bypassSecurityTrustHtml(withBreaks);
  }
}