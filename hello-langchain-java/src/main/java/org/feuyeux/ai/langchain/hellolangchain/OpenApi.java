package org.feuyeux.ai.langchain.hellolangchain;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author feuyeux
 */
public class OpenApi {
  private static final Logger logger = LoggerFactory.getLogger(OpenApi.class);

  public static String getKey() {
    String ak = System.getenv("OPENAI_API_KEY");
    logger.debug("OPENAI_API_KEY:{}", ak);
    return ak;
  }
}
