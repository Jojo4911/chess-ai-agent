import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';

import { App } from './app';
import { Board } from './board/board';

@NgModule({
  declarations: [App, Board],
  imports: [BrowserModule],
  providers: [provideHttpClient()],
  bootstrap: [App],
})
export class AppModule {}
