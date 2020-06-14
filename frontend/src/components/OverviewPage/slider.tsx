import { SFC, ReactNode } from 'react';
import cx from 'classnames';
import Carousel, { ResponsiveType } from 'react-multi-carousel';
import Link from 'next/link';

export interface SliderProps {
    className?: string;
    children: ReactNode;
}

const carouselResponsive: ResponsiveType = {
    superLargeDesktop: {
        breakpoint: { max: 4000, min: 3000 },
        items: 5
    },
    desktop: {
        breakpoint: { max: 3000, min: 1024 },
        items: 3
    },
    tablet: {
        breakpoint: { max: 1024, min: 464 },
        items: 2
    },
    mobile: {
        breakpoint: { max: 464, min: 0 },
        items: 1
    }
};

interface SliderItemProps {
    title: string;
    href: string;
    backgroundImage: string;
}

export const SliderItem: SFC<SliderItemProps> = (props) => (
    <div className="p-2" style={{height: 300}}>
        <Link href={props.href}><a>
            <div className="bg-blue-400 relative h-full bg-cover" style={{
                'backgroundImage': `linear-gradient(to right, rgba(0,0,0,.35), rgba(0,0,0,.35)), url(${props.backgroundImage})`
            }}>
                <h3 className="absolute text-white text-2xl" style={{bottom: '1em', left: '1em'}}>
                    {props.title}</h3>
            </div>
        </a></Link>
    </div>
);

const Slider: SFC<SliderProps> = (props) => (
    <div className={cx('relative', 'pb-8', props.className)}>
        <Carousel
            showDots
            renderDotsOutside
            responsive={carouselResponsive}
        >
            {props.children}
        </Carousel>
    </div>
);

export default Slider;