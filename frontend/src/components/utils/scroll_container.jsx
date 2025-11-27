import React, { useRef, useState, useEffect } from 'react';
import './ScrollableContainer.css'; // Создадим отдельный CSS файл

const ScrollableContainer = ({
                                 children,
                                 maxHeight = 300,
                                 className = '',
                                 showScrollIndicator = true
                             }) => {
    const containerRef = useRef(null);
    const [isScrollable, setIsScrollable] = useState(false);
    const [showTopShadow, setShowTopShadow] = useState(false);
    const [showBottomShadow, setShowBottomShadow] = useState(false);

    useEffect(() => {
        const checkScrollability = () => {
            if (containerRef.current) {
                const element = containerRef.current;
                const hasScroll = element.scrollHeight > element.clientHeight;
                setIsScrollable(hasScroll);

                // Проверяем позицию скролла для теней
                setShowTopShadow(element.scrollTop > 0);
                setShowBottomShadow(
                    element.scrollTop < element.scrollHeight - element.clientHeight
                );
            }
        };

        checkScrollability();

        // Добавляем обработчик ресайза
        const resizeObserver = new ResizeObserver(checkScrollability);
        if (containerRef.current) {
            resizeObserver.observe(containerRef.current);
        }

        return () => {
            resizeObserver.disconnect();
        };
    }, [children, maxHeight]);

    const handleScroll = (e) => {
        const element = e.target;
        setShowTopShadow(element.scrollTop > 0);
        setShowBottomShadow(
            element.scrollTop < element.scrollHeight - element.clientHeight
        );
    };

    return (
        <div className={`scrollable-container-wrapper ${className}`}>
            {showScrollIndicator && isScrollable && (
                <div className="scroll-indicator">
                    Прокрутите для просмотра содержимого
                </div>
            )}

            <div
                ref={containerRef}
                className={`scrollable-container ${isScrollable ? 'scrollable' : ''}`}
                style={{ maxHeight: `${maxHeight}px` }}
                onScroll={handleScroll}
            >
                {showTopShadow && <div className="scroll-shadow top-shadow" />}
                {children}
                {showBottomShadow && <div className="scroll-shadow bottom-shadow" />}
            </div>
        </div>
    );
};

export default ScrollableContainer;