import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';

import rootReducer from '../reducer';

const thunkExtra = {
  apiBase: '/services/learningpage/api/v1'
};

const middleware = [thunk.withExtraArgument(thunkExtra)];

const composeEnhancers =
  typeof window === 'object' &&
  (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ?   
    (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
      // Specify extension’s options like name, actionsBlacklist, actionsCreators, serialize...
    }) : compose;
const store = createStore(rootReducer, composeEnhancers(applyMiddleware(...middleware)));

export default store;