package Package1;

import javax.annotation.Resource;
import javax.xml.bind.JAXBElement;
 
import org.apache.commons.lang.builder.ToStringBuilder;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
 
import com.amdocs.services.fulfillmentorder.fulfillmentorder.FulfillmentOrder;
import com.att.athena.ocx.interfaces.iod.services.FulfillmentOrderDataService;
import com.att.bbnms.logging.Logger;
import com.att.bbnms.logging.LoggerFactory;
 
@Component
@Transactional
public class FulfillmentOrderInboundJmsEndpoint
{
 
   private static final Logger LOG = LoggerFactory.getLoggerWithHostNameAppended(FulfillmentOrderInboundJmsEndpoint.class);
 
   @Resource(name = "fulfillmentOrderDataService")
   private FulfillmentOrderDataService fulfillmentOrderDataService;
 
   @ServiceActivator(inputChannel = "consumeAndProcessFulfillment", outputChannel = "TestOutputchannel")
   public void consumeAndProcessFulfillment(final JAXBElement<FulfillmentOrder> fulfillmentOrder) throws Exception
   {
      LOG.debug("Message retrieved from FulfillmentOrderQueue JMS Queue ==> " + ToStringBuilder.reflectionToString(
            fulfillmentOrder.getValue()));
 
      try
      {
         fulfillmentOrderDataService.processFulfillment(fulfillmentOrder.getValue());
      }
      catch(Exception ex)
      {
         LOG.error("Fulfillment Exception:", ex);
         throw ex;
      }
 
   }
 
}