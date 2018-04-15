import React from 'react';
import ReactDOM from 'react-dom';

import { PDFBookViewer } from './react-book';

const el = document.getElementById('js-pdf'),
  url = el.getAttribute('data-url'),
  workerSrc = el.getAttribute('data-worker');

ReactDOM.render(
  <PDFBookViewer url={url} workerSrc={workerSrc} />,
  el
);
