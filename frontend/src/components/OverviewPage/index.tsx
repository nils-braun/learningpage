import { SFC } from 'react';

import Slider, { SliderItem } from './slider';

export interface OverviewPageProps {}

const bgImage = 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://s3.amazonaws.com/coursera_assets/browse/domains/data_science.png?auto=format%2Ccompress&dpr=3&w=&h=&fit=crop';

const OverviewPage: SFC<OverviewPageProps> = (props) => (
    <div className="container mx-auto">
        <h2 className="text-2xl font-thin">Explore Courses</h2>
        <Slider className="my-4">
            <SliderItem title="Data Engineer Expert" href="/courses/dex" backgroundImage={bgImage} />
            <SliderItem title="Data Analyst Expert" href="/courses/dax" backgroundImage={bgImage} />
            <SliderItem title="Data Scientist Expert" href="/courses/dsx" backgroundImage={bgImage} />
            <SliderItem title="Data Science Beginner" href="/courses/dsb" backgroundImage={bgImage} />
            <SliderItem title="Data Science Advanced" href="/courses/dsa" backgroundImage={bgImage} />
        </Slider>
        <h2 className="text-2xl font-thin">Popular courses</h2>
        <Slider className="my-4">
            <SliderItem title="Data Engineer Expert" href="/courses/dex" backgroundImage={bgImage} />
            <SliderItem title="Data Analyst Expert" href="/courses/dax" backgroundImage={bgImage} />
            <SliderItem title="Data Scientist Expert" href="/courses/dsx" backgroundImage={bgImage} />
            <SliderItem title="Data Science Beginner" href="/courses/dsb" backgroundImage={bgImage} />
            <SliderItem title="Data Science Advanced" href="/courses/dsa" backgroundImage={bgImage} />
        </Slider>
    </div>
);
  
export default OverviewPage