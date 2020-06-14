import { SFC, useEffect } from 'react';
import { connect, ConnectedProps } from 'react-redux';

import { thunkFetchUser } from '../../actions/user';
import { RootState } from '../../types';

export interface UserInfoOwnProps {}

const mapState = (state: RootState) => ({});
const mapDispatch = {
    onInit: thunkFetchUser
};

const connector = connect(mapState, mapDispatch);

type UserInfoPropsFromRedux = ConnectedProps<typeof connector>;

export type UserInfoProps = UserInfoPropsFromRedux & UserInfoOwnProps;

/**
 * This component does not render any content on its own.
 * It's purpose is to load content that can not be pre-rendered, but must be
 * load form the client side.
 * So it only has side-effects that update the Redux store.
 */
const UserInfo: SFC<UserInfoProps> = (props) => {
    useEffect(() => {
        props.onInit();
    });
    return null;
}

export default connector(UserInfo);
