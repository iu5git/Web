import { Tobacco } from "types/tobacco";

export type CoffeeCardProps = Omit<
    React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>,
    "ref"
> & {
    tobacco: Tobacco;
};
