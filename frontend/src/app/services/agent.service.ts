import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AskRequest, AskResponse } from '../models/agent.models';

@Injectable({ providedIn: 'root' })
export class AgentService {
  private readonly baseUrl = '/api/v1';

  constructor(private http: HttpClient) {}

  ask(question: string, fen?: string): Observable<AskResponse> {
    const body: AskRequest = { question, ...(fen ? { fen } : {}) };
    return this.http.post<AskResponse>(`${this.baseUrl}/agent/ask`, body);
  }
}