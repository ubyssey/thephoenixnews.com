import React from 'react';

export default function GallerySlide(props) {
  const slideStyle = { width: props.width };
  const imageStyle = { backgroundImage: `url('${props.src}')` };

  return (
    <li className="slide" style={slideStyle}>
      <div className="inner">
        <div className="image">
          <div>
            <div className="img" style={imageStyle}></div>
          </div>
        </div>
        <div className='slide-meta'>
          { props.caption &&
            <p className="slide-caption" dangerouslySetInnerHTML={{__html: this.props.caption}}></p> }
          { props.credit &&
            <p className="slide-credit" dangerouslySetInnerHTML={{__html: this.props.credit}}></p> }
        </div>
      </div>
    </li>
  );
}
