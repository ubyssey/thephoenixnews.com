import React from 'react';
import Gallery from './Gallery';

export default function Galleries(props) {
  const galleries = props.galleries.map((gallery, i) => {
    return (
      <Gallery
        key={i}
        title={gallery.title}
        selector={gallery.selector}
        images={gallery.list}
        imagesTable={gallery.table} />
    );
  });

  return <div>{galleries}</div>
}
