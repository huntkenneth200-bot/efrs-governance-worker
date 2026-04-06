import { registerSchema } from "./SchemaRegistry";
import { DGEProcessRequestSchema } from "./schemas/DGEProcessRequest.schema";
import { DGEProcessResponseSchema } from "./schemas/DGEProcessResponse.schema";
import { LGEUpdateRequestSchema } from "./schemas/LGEUpdateRequest.schema";
import { LGEUpdateResponseSchema } from "./schemas/LGEUpdateResponse.schema";
import { DocumentEventSchema } from "./schemas/DocumentEvent.schema";

export function bootstrapSchemas() {
  registerSchema("DGEProcessRequest", DGEProcessRequestSchema);
  registerSchema("DGEProcessResponse", DGEProcessResponseSchema);
  registerSchema("LGEUpdateRequest", LGEUpdateRequestSchema);
  registerSchema("LGEUpdateResponse", LGEUpdateResponseSchema);
  registerSchema("DocumentEvent", DocumentEventSchema);
}
