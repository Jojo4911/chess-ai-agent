export interface AskRequest {
  question: string;
  fen?: string;
}

export interface ToolCall {
  tool: string;
  input: Record<string, unknown>;
  output: string;
}

export interface AskResponse {
  answer: string;
  tool_calls: ToolCall[];
}