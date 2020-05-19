import { dummyPageContent } from '../../dummy_data';
import CoursePage from '../../components/CoursePage';

export async function getServerSideProps({ query }) {
  const { slug } = query;
  // TODO: Does not work because credentials are only available in client.
  //       We cannot use server-side rendering in this case.
  // const url = `http://127.0.0.1:8000/services/learningpage/api/v1/content/${slug}`;
  // await fetch(url, { method: 'GET', credentials: 'include' })
  //   .then(res => res.json())
  //   .then(content => console.log(content))
  //   .catch(err => console.error(err));
  return { props: { content: dummyPageContent } }
}

export default CoursePage;