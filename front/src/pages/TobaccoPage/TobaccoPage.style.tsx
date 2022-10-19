import { COLORS } from "constants/colors";
import styled from "styled-components";

export const TobaccoPageStyled = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100vw;
    height: 100vh;
    background-color: ${COLORS.BackgroundDark};
    color: ${COLORS.TextGrey};

    h1 {
        margin-top: 40px;
        font-size: 50px;
    }
    h2 {
        margin-top: 20px;
    }
`;

export const ButtonStyled = styled.button`
    margin-top: 20px;
    border: none;
    width: 300px;
    height: 40px;
    background-color: ${COLORS.BorderColor};
    cursor: pointer;
    color: ${COLORS.TextGrey};
    font-size: large;
`;
