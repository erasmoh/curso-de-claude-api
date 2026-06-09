import { z } from "zod";

export const InvoiceData = z.object({
  provider: z.string().nullable(),
  date: z.string().nullable(),
  currency: z.string().nullable(),
  total: z.number().nullable(),
  items: z.array(z.object({
    description: z.string(),
    quantity: z.number().nullable().optional(),
    unit_price: z.number().nullable().optional(),
    total: z.number(),
  })),
});
