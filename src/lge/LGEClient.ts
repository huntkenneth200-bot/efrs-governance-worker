import type { ApiResponse, VersionedDto } from "../contracts";

export interface LgeLexiconRequest extends VersionedDto {
  tenantId: string;
  lexiconName: string;
  input: string;
}

export interface LgeLexiconResult extends VersionedDto {
  tenantId: string;
  lexiconName: string;
  output: string;
  tokensUsed?: number;
}

export interface LGEClient {
  resolve(
    request: LgeLexiconRequest
  ): Promise<ApiResponse<LgeLexiconResult>>;
}
