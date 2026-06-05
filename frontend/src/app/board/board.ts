import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Chess } from 'chess.js';

const PIECE_SYMBOL: Record<string, string> = {
  wk: '♔', wq: '♕', wr: '♖', wb: '♗', wn: '♘', wp: '♙',
  bk: '♚', bq: '♛', br: '♜', bb: '♝', bn: '♞', bp: '♟',
};

const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
const RANKS = [8, 7, 6, 5, 4, 3, 2, 1];

interface Cell {
  square: string;
  piece: string | null;
  isLight: boolean;
  isSelected: boolean;
  isTarget: boolean;
}

@Component({
  selector: 'app-board',
  standalone: false,
  templateUrl: './board.html',
  styleUrls: ['./board.css'],
})
export class Board implements OnInit {
  @Output() fenChange = new EventEmitter<string>();

  private chess = new Chess();
  grid: Cell[][] = [];
  private selected: string | null = null;
  private targets = new Set<string>();

  ngOnInit(): void {
    this.rebuildGrid();
  }

  getFen(): string {
    return this.chess.fen();
  }

  onCellClick(cell: Cell): void {
    if (this.selected && this.targets.has(cell.square)) {
      this.chess.move({ from: this.selected, to: cell.square, promotion: 'q' });
      this.selected = null;
      this.targets.clear();
      this.rebuildGrid();
      this.fenChange.emit(this.chess.fen());
      return;
    }

    const piece = this.chess.get(cell.square as any);
    if (piece && piece.color === this.chess.turn()) {
      this.selected = cell.square;
      this.targets = new Set(
        this.chess.moves({ square: cell.square as any, verbose: true }).map((m: any) => m.to)
      );
    } else {
      this.selected = null;
      this.targets.clear();
    }
    this.applyHighlights();
  }

  getSymbol(piece: string | null): string {
    return piece ? (PIECE_SYMBOL[piece] ?? '') : '';
  }

  private rebuildGrid(): void {
    this.grid = RANKS.map((rank) =>
      FILES.map((file) => {
        const square = `${file}${rank}`;
        const piece = this.chess.get(square as any);
        return {
          square,
          piece: piece ? `${piece.color}${piece.type}` : null,
          isLight: (FILES.indexOf(file) + rank) % 2 !== 0,
          isSelected: false,
          isTarget: false,
        };
      })
    );
  }

  private applyHighlights(): void {
    this.grid.forEach((row) =>
      row.forEach((cell) => {
        cell.isSelected = cell.square === this.selected;
        cell.isTarget = this.targets.has(cell.square);
      })
    );
  }
}