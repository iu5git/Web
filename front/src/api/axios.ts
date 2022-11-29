import axios from "axios";
import { BACKEND_URL } from "config";

export const axiosInstance = axios.create({
    baseURL: BACKEND_URL,
});
