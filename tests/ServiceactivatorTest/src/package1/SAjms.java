package Package1;

import javax.annotation.Resource;
import javax.xml.bind.JAXBElement;
 
import org.apache.commons.lang.builder.ToStringBuilder;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.annotation.Transformer;
import org.springframework.integration.annotation.Gateway;
import org.springframework.integration.annotation.MessagingGateway;
import org.springframework.integration.annotation.Filter;
import org.springframework.integration.annotation.Router;
import org.springframework.integration.annotation.Splitter;
import org.springframework.integration.annotation.Aggregator;
import org.springframework.integration.annotation.InboundChannelAdapter;
import org.springframework.integration.annotation.Publisher;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
 
import com.fulfillmentorder.fulfillmentorder.FulfillmentOrder;
import com.services.FulfillmentOrderDataService;
import com.Logger;
import com.LoggerFactory;
 
@Component
@Transactional
public class FulfillmentOrderInboundJmsEndpoint
{
 
   private static final Logger LOG = LoggerFactory.getLoggerWithHostNameAppended(FulfillmentOrderInboundJmsEndpoint.class);
 
   @Resource(name = "fulfillmentOrderDataService")
   private FulfillmentOrderDataService fulfillmentOrderDataService;
   
   @Bean
   @Transformer(inputChannel="fromTcp", outputChannel="toHandler")
   JsonToObjectTransformer jsonToObjectTransformer() {
       return new JsonToObjectTransformer(MyObject.class);
   }
   
   @Router(inputChannel="routingChannel")
   public String route(Object payload) {
      
    }
   
   
   
    @Gateway(requestChannel="orders")
    public String placeOrder(Order order) {
    
    }
    
    @InboundChannelAdapter(Channel="inbound")
    public String inboundplaceOrder(Order order) {
    
    }
    
    @Publisher(Channel="publish")
    public String publishOrder(Order order) {
    
    }
    
    @MessagingGateway(defaultRequestChannel="msgorders", defaultReplyChannel="replyorders")
    public String msgplaceOrder(Order order) {
    
    }

   
   
   @Splitter(inputChannel = "tosplitterChannel", outputChannel = "tooutsplitterChannel")
   public List<Message<?>> splitIntoMessages(final List<EmailFragment> emailFragments) {

   	final List<Message<?>> messages = new ArrayList<Message<?>>();

   	for (EmailFragment emailFragment : emailFragments) {
   		Message<?> message = MessageBuilder.withPayload(emailFragment.getData())
   										.setHeader(FileHeaders.FILENAME, emailFragment.getFilename())
   										.setHeader("directory", emailFragment.getDirectory())
   										.build();
   		messages.add(message);
   	}

   	return messages;
   }
   
   @Aggregator(inputChannel = "toAggregatorChannel", outputChannel = "toRouterChannel", discardChannel = "nullChannel")
   public List<File> aggregate(List<File> files){
       return files;
   }
 
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