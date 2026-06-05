import { Component, ChangeDetectorRef } from '@angular/core';
import { AgentService } from './services/agent.service';
import { AskResponse } from './models/agent.models';

@Component({
  selector: 'app-root',
  standalone: false,
  templateUrl: './app.html',
  styleUrls: ['./app.css'],
})
export class App {
  currentFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  response: AskResponse | null = null;
  loading = false;
  error = '';

  constructor(
    private agentService: AgentService,
    private cdr: ChangeDetectorRef,
  ) {}

  onFenChange(fen: string): void {
    this.currentFen = fen;
  }

  onAsk(question: string): void {
    if (!question.trim()) return;
    this.loading = true;
    this.error = '';
    this.response = null;
    this.agentService.ask(question, this.currentFen).subscribe({
      next: (res) => {
        this.response = res;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = "Erreur lors de la communication avec l'agent.";
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }
}