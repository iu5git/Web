import { ActionCreatorWithoutPayload, createSlice, SliceCaseReducers } from "@reduxjs/toolkit";
import {
    createTobaccoAction,
    deleteTobaccoAction,
    getTobaccoByIdAction,
    getTobaccoListAction,
} from "store/tobaccos/tobaccos.action";
import { Tobacco } from "types/tobacco";

export interface TobaccoState {
    tobacco?: Tobacco;
    tobaccos?: Tobacco[];
    error: unknown;
}

const initialState: TobaccoState = {
    tobacco: undefined,
    tobaccos: [],
    error: undefined,
};

const tobaccoSlice = createSlice<TobaccoState, SliceCaseReducers<TobaccoState>>({
    name: "tobacco",
    initialState,
    reducers: {
        reset: () => initialState,
    },
    extraReducers: (builder) => {
        builder.addCase(createTobaccoAction.pending, (state) => {
            state.error = null;
        });
        builder.addCase(createTobaccoAction.fulfilled, (state, { payload }) => {
            state.tobacco = payload;
        });
        builder.addCase(createTobaccoAction.rejected, (state, { error }) => {
            state.error = error;
        });

        builder.addCase(getTobaccoListAction.pending, (state) => {
            state.error = null;
        });
        builder.addCase(getTobaccoListAction.fulfilled, (state, { payload }) => {
            state.tobaccos = payload;
        });
        builder.addCase(getTobaccoListAction.rejected, (state, { error }) => {
            state.error = error;
        });

        builder.addCase(getTobaccoByIdAction.pending, (state) => {
            state.error = null;
        });
        builder.addCase(getTobaccoByIdAction.fulfilled, (state, { payload }) => {
            state.tobacco = payload;
        });
        builder.addCase(getTobaccoByIdAction.rejected, (state, { error }) => {
            state.error = error;
        });

        builder.addCase(deleteTobaccoAction.pending, (state) => {
            state.error = null;
        });
        builder.addCase(deleteTobaccoAction.fulfilled, (state) => {});
        builder.addCase(deleteTobaccoAction.rejected, (state, { error }) => {
            state.error = error;
        });
    },
});

export const resetTobaccoState = tobaccoSlice.actions.reset as ActionCreatorWithoutPayload<string>;
export const tobaccoReducer = tobaccoSlice.reducer;
