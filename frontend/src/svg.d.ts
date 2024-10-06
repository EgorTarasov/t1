declare module "*.svg" {
  const content: React.FC<HTMLProps<SVGElement>>;
  export default content;
}

declare module "*.css" {
  const content: Record<string, string>;
  export default content;
}
