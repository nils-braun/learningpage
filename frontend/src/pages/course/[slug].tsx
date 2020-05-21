import CoursePage, { CoursePageProps } from '../../components/CoursePage';
import { apiBaseUrl } from '../../utils';
import { ApiCoursePage } from '../../types';
import { GetServerSideProps } from 'next';

export const getServerSideProps: GetServerSideProps<CoursePageProps> = async context => {
  const { slug } = context.query;
  const url = [apiBaseUrl, 'content', slug].join('/');
  const page: ApiCoursePage = await fetch(url, { method: 'GET' })
    .then(res => res.json())
    .catch(err => console.error(err));
  return { props: { page } }
}

export default CoursePage;