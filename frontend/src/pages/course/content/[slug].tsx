import CoursePage, { CoursePageOwnProps } from '../../../components/CoursePage';
import { apiBaseUrl } from '../../../utils';
import { ApiCoursePage } from '../../../types';
import { GetServerSideProps } from 'next';

export const getServerSideProps: GetServerSideProps<CoursePageOwnProps> = async ({ res, query }) => {
  const url = [apiBaseUrl, 'content', query.slug].join('/');
  const page: ApiCoursePage = await fetch(url, { method: 'GET' })
    .then(res => res.json())
    .catch(err => console.error(err));
    
  if (!page) {
    res.statusCode = 404;
    res.end('Not found');
    return;
  }

  return { props: { page  } }
}

export default CoursePage;