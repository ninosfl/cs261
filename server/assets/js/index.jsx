/* jshint esversion: 6 */

import React from 'react';
import ReactDOM from 'react-dom';
import { YearList, MonthList, DayList } from './list-reports';
import { ErrorMessage } from './errors';
import { SearchBar } from './searchbar';

// Try different render targets, rendering to the one that appears first
let target = null;

if (target = document.querySelector('#searchbar')){
  ReactDOM.render(<SearchBar />, target)
}

if (target = document.querySelector('#report-list-years')) {
  ReactDOM.render(<YearList />, target);
} else if (target = document.querySelector('#report-list-months')) {
  ReactDOM.render(<MonthList />, target);
} else if (target = document.querySelector('#report-list-days')) {
  ReactDOM.render(<DayList />, target);
}

if (target = document.querySelector('#error-root')) {
  ReactDOM.render(<ErrorMessage />, target);
} 
