import CoursePage from '../../components/CoursePage';
import { apiBaseUrl } from '../../utils';
import { ApiCoursePage } from '../../types';

export async function getServerSideProps({ query }) {
  const { slug } = query;
  const url = [apiBaseUrl, 'content', slug].join('/');
  const content: ApiCoursePage = await fetch(url, { method: 'GET' })
    .then(res => res.json())
    .catch(err => console.error(err));
  return { props: { content } }
}

export default CoursePage;