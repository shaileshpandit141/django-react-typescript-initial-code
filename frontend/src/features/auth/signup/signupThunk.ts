import { createAsyncThunk } from "@reduxjs/toolkit";
import API from 'API';
import {
  SignupSuccessResponse,
  SignupErrorResponse
} from "./signup.types";
import { SignupCredentials } from 'API/API.types';
import { CatchAxiosError } from 'FeatureTypes';

/**
 * Redux thunk to handle user signup process
 *
 * @param credentials - User signup credentials (email, password, etc)
 * @returns SignupSuccessResponse on successful signup
 * @throws SignupErrorResponse on signup failure
 */
export const signupThunk = createAsyncThunk(
  "signup/signupThunk",
  async (credentials: SignupCredentials, thunkAPI) => {
    try {
      // Call signup API endpoint
      const response = await API.signupApi(credentials);
      return response.data as SignupSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse: SignupErrorResponse;

      // Handle API error response or create generic error
      if (error.response) {
        errorResponse = error.response.data;
      } else {
        errorResponse = {
          status: "failed",
          message: error.message ?? "An unknown error occurred",
          errors: {
            non_field_errors: [error.message ?? "An unknown error occurred"],
          },
        };
      }
      return thunkAPI.rejectWithValue(errorResponse);
    }
  }
);
