export type Tobacco = {
    id: number;
    title: string;
    price: number;
};

export type CoffeeCardProps = Omit<
    React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>,
    "ref"
> & {
    tobacco: Tobacco;
};
