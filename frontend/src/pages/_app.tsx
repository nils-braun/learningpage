import '../styles/index.css'

import { Provider } from 'react-redux'
import Head from 'next/head';

import store from '../store'
import UserInfo from '../components/UserInfo';

export default function MyApp({ Component, pageProps }) {
  return (
    <Provider store={store}>
        <Head>
          <link rel="stylesheet" href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css" />
        </Head>
        <UserInfo />
        <Component {...pageProps} />
    </Provider>
  );
}
