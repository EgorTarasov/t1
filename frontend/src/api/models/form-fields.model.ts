import { z } from "zod";

export namespace FormFieldsDto {
  export const Template = z.record(
    z.object({
      description: z.string().optional(),
      value: z.union([z.literal("int"), z.literal("string")]),
      title: z.string(),
    }),
  );
  export type Template = z.infer<typeof Template>;
}
