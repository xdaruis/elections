import { createSlice } from '@reduxjs/toolkit';

import setAuthToken from '../utils/setAuthToken';

const initialState = {
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  username: null,
  isLoading: true
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action) => {
      const { token, username } = action.payload;
      setAuthToken(token);
      state.token = token;
      state.username = username;
      state.isLoading = false;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      setAuthToken();
      state.token = null;
      state.username = null;
      state.isLoading = false;
      state.isAuthenticated = false;
      localStorage.removeItem('token');
    },
    loaded: (state) => {
      state.isLoading = false;
    }
  }
});

export const { login, logout, loaded } = authSlice.actions;

export default authSlice.reducer;
