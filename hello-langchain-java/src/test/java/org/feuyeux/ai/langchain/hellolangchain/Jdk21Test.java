package org.feuyeux.ai.langchain.hellolangchain;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

@Slf4j
public class Jdk21Test {

  @Test
  public void test() {
    log.debug("Hello, Java 21!");
    log.info("Hello, Java 21!");
    log.warn("Hello, Java 21!");
    log.error("Hello, Java 21!");
  }
}
