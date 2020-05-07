import { dummyPageContent } from '../../dummy_data';
import CoursePage from '../../components/CoursePage';

export async function getServerSideProps() {
  return { props: { content: dummyPageContent } }
}

export default CoursePage;