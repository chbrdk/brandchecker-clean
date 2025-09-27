import React, { useState, useRef, useEffect } from 'react';
import { Icon } from '../Icon';
import './Carousel.css';

export interface CarouselProps {
  children: React.ReactNode;
  itemsPerView?: number;
  showArrows?: boolean;
  showDots?: boolean;
  autoPlay?: boolean;
  autoPlayInterval?: number;
  loop?: boolean;
  className?: string;
  onSlideChange?: (currentIndex: number) => void;
}

export const Carousel = ({
  children,
  itemsPerView = 1,
  showArrows = true,
  showDots = true,
  autoPlay = false,
  autoPlayInterval = 3000,
  loop = true,
  className = '',
  onSlideChange
}: CarouselProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const carouselRef = useRef<HTMLDivElement>(null);
  const autoPlayRef = useRef<NodeJS.Timeout | null>(null);

  const childrenArray = React.Children.toArray(children);
  const totalItems = childrenArray.length;
  const maxIndex = Math.max(0, totalItems - itemsPerView);

  // Auto-play functionality
  useEffect(() => {
    if (autoPlay && totalItems > itemsPerView) {
      autoPlayRef.current = setInterval(() => {
        nextSlide();
      }, autoPlayInterval);

      return () => {
        if (autoPlayRef.current) {
          clearInterval(autoPlayRef.current);
        }
      };
    }
  }, [autoPlay, autoPlayInterval, totalItems, itemsPerView]);

  // Pause auto-play on hover
  const handleMouseEnter = () => {
    if (autoPlayRef.current) {
      clearInterval(autoPlayRef.current);
    }
  };

  const handleMouseLeave = () => {
    if (autoPlay && totalItems > itemsPerView) {
      autoPlayRef.current = setInterval(() => {
        nextSlide();
      }, autoPlayInterval);
    }
  };

  const goToSlide = (index: number) => {
    if (isTransitioning) return;
    
    setIsTransitioning(true);
    setCurrentIndex(index);
    
    if (onSlideChange) {
      onSlideChange(index);
    }

    setTimeout(() => {
      setIsTransitioning(false);
    }, 300);
  };

  const nextSlide = () => {
    if (isTransitioning) return;
    
    if (currentIndex >= maxIndex) {
      if (loop) {
        goToSlide(0);
      }
    } else {
      goToSlide(currentIndex + 1);
    }
  };

  const prevSlide = () => {
    if (isTransitioning) return;
    
    if (currentIndex <= 0) {
      if (loop) {
        goToSlide(maxIndex);
      }
    } else {
      goToSlide(currentIndex - 1);
    }
  };

  const canGoNext = loop || currentIndex < maxIndex;
  const canGoPrev = loop || currentIndex > 0;

  const classes = [
    'carousel',
    className
  ].filter(Boolean).join(' ');

  return (
    <div 
      className={classes}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="carousel__container">
        {showArrows && canGoPrev && (
          <button
            className="carousel__arrow carousel__arrow--prev"
            onClick={prevSlide}
            disabled={isTransitioning}
            aria-label="Previous slide"
          >
            <Icon name="chevron-left" size="sm" />
          </button>
        )}

        <div className="carousel__track" ref={carouselRef}>
          <div 
            className="carousel__slides"
            style={{
              transform: `translateX(-${(currentIndex * 100) / itemsPerView}%)`,
              transition: isTransitioning ? 'transform 0.3s ease-in-out' : 'none'
            }}
          >
            {childrenArray.map((child, index) => (
              <div
                key={index}
                className="carousel__slide"
                style={{
                  width: `${100 / itemsPerView}%`,
                  flexShrink: 0
                }}
              >
                {child}
              </div>
            ))}
          </div>
        </div>

        {showArrows && canGoNext && (
          <button
            className="carousel__arrow carousel__arrow--next"
            onClick={nextSlide}
            disabled={isTransitioning}
            aria-label="Next slide"
          >
            <Icon name="chevron-right" size="sm" />
          </button>
        )}
      </div>

      {showDots && totalItems > itemsPerView && (
        <div className="carousel__dots">
          {Array.from({ length: maxIndex + 1 }, (_, index) => (
            <button
              key={index}
              className={`carousel__dot ${index === currentIndex ? 'carousel__dot--active' : ''}`}
              onClick={() => goToSlide(index)}
              disabled={isTransitioning}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
};

Carousel.displayName = 'Carousel';
