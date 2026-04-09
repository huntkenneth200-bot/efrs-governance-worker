"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.bootstrapSchemas = bootstrapSchemas;
const SchemaRegistry_1 = require("./SchemaRegistry");
const DGEProcessRequest_schema_1 = require("./schemas/DGEProcessRequest.schema");
const DGEProcessResponse_schema_1 = require("./schemas/DGEProcessResponse.schema");
const LGEUpdateRequest_schema_1 = require("./schemas/LGEUpdateRequest.schema");
const LGEUpdateResponse_schema_1 = require("./schemas/LGEUpdateResponse.schema");
const DocumentEvent_schema_1 = require("./schemas/DocumentEvent.schema");
function bootstrapSchemas() {
    (0, SchemaRegistry_1.registerSchema)("DGEProcessRequest", DGEProcessRequest_schema_1.DGEProcessRequestSchema);
    (0, SchemaRegistry_1.registerSchema)("DGEProcessResponse", DGEProcessResponse_schema_1.DGEProcessResponseSchema);
    (0, SchemaRegistry_1.registerSchema)("LGEUpdateRequest", LGEUpdateRequest_schema_1.LGEUpdateRequestSchema);
    (0, SchemaRegistry_1.registerSchema)("LGEUpdateResponse", LGEUpdateResponse_schema_1.LGEUpdateResponseSchema);
    (0, SchemaRegistry_1.registerSchema)("DocumentEvent", DocumentEvent_schema_1.DocumentEventSchema);
}
//# sourceMappingURL=SchemaBootstrap.js.map