import { COLORS } from "constants/colors";
import styled from "styled-components";

export const TobaccoCardStyled = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 4px;
    border: 1px solid ${COLORS.BorderColor};
    cursor: pointer;
    width: 100%;
    color: ${COLORS.TextGrey};
    padding: 16px;
    transition: all 0.2s;

    h2 {
        padding: 0;
        font-size: 30px !important;
    }

    p {
        font-size: 20px;
    }

    &:hover {
        border: 1px solid ${COLORS.BorderColor};
        transform: scale(1.01, 1.01);
    }
`;
