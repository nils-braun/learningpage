import { SFC } from 'react';

import Header from '../components/Header';
import OverviewPage from '../components/OverviewPage';

interface PageProps {}

const Page: SFC<PageProps> = (props) => (
    <div className="bg-gray-100 h-screen">
        <Header />
        <OverviewPage />
    </div>
);
  
export default Page
  