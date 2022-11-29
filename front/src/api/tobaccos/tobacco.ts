import { axiosInstance } from "api/axios";
import { Tobacco } from "types/tobacco";
import { AxiosError, AxiosResponse } from "axios";

const baseUrl = "/products";

export const getTobaccoList = (): Promise<Tobacco[]> =>
    axiosInstance
        .get<Tobacco, AxiosResponse<Tobacco[]>>(`${baseUrl}/`)
        .then((res) => res.data)
        .catch((err: AxiosError<Record<string, string>>) => {
            throw JSON.stringify(err.response?.data);
        });

export const getTobaccoById = (id: string): Promise<Tobacco> =>
    axiosInstance
        .get<Tobacco, AxiosResponse<Tobacco>>(`${baseUrl}/${id}`)
        .then((res) => res.data)
        .catch((err: AxiosError<Record<string, string>>) => {
            throw JSON.stringify(err.response?.data);
        });

export const createTobacco = (coffee: Omit<Tobacco, "id">): Promise<Tobacco> =>
    axiosInstance
        .post<Tobacco, AxiosResponse<Tobacco>>(`${baseUrl}/`, coffee)
        .then((res) => res.data)
        .catch((err: AxiosError<Record<string, string>>) => {
            throw JSON.stringify(err.response?.data);
        });

export const deleteTobacco = (id: string): Promise<Tobacco> =>
    axiosInstance
        .delete<Tobacco, AxiosResponse<Tobacco>>(`${baseUrl}/${id}`)
        .then((res) => res.data)
        .catch((err: AxiosError<Record<string, string>>) => {
            throw JSON.stringify(err.response?.data);
        });
