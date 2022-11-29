import { createAsyncThunk } from "@reduxjs/toolkit";
import { createTobacco, deleteTobacco, getTobaccoById, getTobaccoList } from "api/tobaccos";
import { Tobacco } from "types/tobacco";

export const createTobaccoAction = createAsyncThunk("tobaccos/createTobacco", async (tobacco: Tobacco) => {
    return await createTobacco(tobacco);
});

export const getTobaccoListAction = createAsyncThunk("tobaccos/getTobaccoList", async () => {
    return await getTobaccoList();
});

export const deleteTobaccoAction = createAsyncThunk("tobaccos/deleteTobacco", async (id: string) => {
    return await deleteTobacco(id);
});

export const getTobaccoByIdAction = createAsyncThunk("tobaccos/getTobaccoById", async (id: string) => {
    return await getTobaccoById(id);
});
